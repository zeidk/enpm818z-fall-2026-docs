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
      How close a measurement is to the true value. Distinct from
      precision, which describes repeatability. A sensor with a steady
      offset can be highly precise and still inaccurate. See Bias.
      :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

   ADAS
      Advanced Driver Assistance Systems. Systems that support the human
      driver in performing parts of the Dynamic Driving Task. Corresponds
      to SAE Levels 1--2. Examples: Adaptive Cruise Control, Lane Keeping
      Assist. :doc:`L1 </lectures/lecture1/l1_lecture>`

   ADS
      Automated Driving Systems. Systems that perform the entire Dynamic
      Driving Task without human intervention within a specified ODD.
      Corresponds to SAE Levels 3--5. Not to be confused with UMD's
      Accessibility and Disability Service, which shares the abbreviation. :doc:`L1 </lectures/lecture1/l1_lecture>`

   AEB
      Automatic Emergency Braking. A momentary intervention that applies the
      brakes to avoid or mitigate a collision. Despite taking control of the
      vehicle it is classified as **SAE Level 0**, because the human never
      stops performing the DDT. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Anchor Box
      A predefined bounding box shape (width, height) used by object
      detectors like YOLO v3--v7 as a reference for predicting object
      locations. Anchor-free detectors (YOLOv8+, DETR) eliminate these. :doc:`L4 </lectures/lecture4/l4_index>`

   A* Search
      A heuristic graph-search algorithm that finds the shortest path from
      start to goal by expanding the node with the lowest :math:`f(n) =
      g(n) + h(n)`, where :math:`g` is the cost so far and :math:`h` is an
      admissible heuristic. Used for global route planning on the road
      graph and for grid/lattice-based motion planning. :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`L10 </lectures/lecture10/l10_index>`

   Angular Resolution
      The smallest angular separation at which two returns can still be
      told apart. Because it is an angle, the width it covers grows with
      range: 2 degrees spans 3.5 m at 100 m, which is a car and the
      motorcycle beside it. :doc:`L2 </lectures/lecture2/l2_index>`

   ASIL
      Automotive Safety Integrity Level. Defined by ISO 26262 to classify
      the severity of safety risks. Ranges from ASIL A (lowest) to ASIL D
      (highest), determining the rigor of development and testing required. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   ASPP
      Atrous Spatial Pyramid Pooling. The multi-scale context module in
      DeepLabv3+ that applies parallel dilated convolutions at several
      rates (e.g., 6, 12, 18) and pools at multiple scales, then
      concatenates the outputs -- capturing objects at varying scales in
      a single forward pass. :doc:`L5 </lectures/lecture5/l5_index>`


.. _glossary-b:

B
=

.. glossary::

   Backbone
      The feature extraction component of an object detection architecture.
      In YOLO, this is typically CSPDarknet or similar CNN that extracts
      hierarchical features from the input image. :doc:`L4 </lectures/lecture4/l4_index>`

   Baseline
      The distance between the two optical centres of a stereo pair,
      written B. Depth error grows as z squared over Bf, so the baseline
      is the only term a designer controls, and it is bounded by the
      width of the vehicle. :doc:`L2 </lectures/lecture2/l2_index>`

   Bayer Pattern
      The colour filter array placed over a monochrome camera sensor
      (typically RGGB) so that each pixel records only one colour channel.
      Demosaicing reconstructs full RGB images. Determines per-channel
      resolution and low-light noise behaviour. :doc:`L2 </lectures/lecture2/l2_index>`

   Behavior Cloning
      An imitation learning approach where a policy is trained by supervised
      regression on expert state-action pairs. Simple but suffers from
      distribution shift and compounding errors that grow as
      :math:`O(\epsilon T^2)`. :doc:`L12 </lectures/lecture12/l12_index>`

   Behavior Planning
      The strategic decision-making layer that selects high-level maneuvers
      (lane follow, lane change, yield, stop) based on the current driving
      context. Often implemented as a finite state machine (FSM). :doc:`L9 </lectures/lecture9/l9_index>`

   Belief
      Everything a filter currently knows about the state, expressed as
      a mean and a covariance. A Kalman filter's belief always has a
      single peak. A particle filter's belief can have several. :doc:`L3
      </lectures/lecture3/l3_index>`

   BEV
      Bird's-Eye View. A top-down representation of the driving scene that
      projects sensor data into an ego-centric 2D plane. The dominant
      perception paradigm in modern AV systems. See also: BEVFormer. :doc:`L5 </lectures/lecture5/l5_index>`

   BEVFormer
      A transformer-based BEV construction method (Li et al., ECCV 2022)
      that uses learnable BEV queries with spatial cross-attention and
      temporal self-attention to build BEV features from multi-camera images. :doc:`L5 </lectures/lecture5/l5_index>`

   BEVFusion
      A multi-sensor BEV fusion framework that unifies camera and LiDAR
      features in a shared BEV space using learned attention-weighted
      aggregation. :doc:`L6 </lectures/lecture6/l6_index>`

   Bias
      A systematic error that shifts every reading the same way. Unlike
      noise it does not average away, and a Kalman filter does not
      remove it, because it breaks the zero-mean assumption. Two sensors
      can have identical variance and very different bias. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

   Bicycle Model
      A simplified kinematic vehicle model that merges the two front wheels
      and two rear wheels into single virtual wheels. Used as the foundation
      for motion planning and control. :doc:`L10 </lectures/lecture10/l10_index>` · :doc:`L11 </lectures/lecture11/l11_index>`

   Bipartite Matching
      The Hungarian algorithm used by DETR to find an optimal one-to-one
      assignment between predicted objects and ground truth during training.
      Eliminates the need for NMS. :doc:`L4 </lectures/lecture4/l4_index>`

   Blueprint Library
      In CARLA, a collection of templates for creating actors (vehicles,
      pedestrians, sensors) with configurable attributes like color and
      sensor parameters. :doc:`L1 </lectures/lecture1/l1_lecture>`

   B-Spline
      A piecewise polynomial curve with local control point support, used
      for smooth trajectory representation in motion planning. Changes to
      one control point only affect a local segment of the curve. :doc:`L11 </lectures/lecture11/l11_index>`

   ByteTrack
      A multi-object tracking method (Zhang et al., 2022) that recovers
      occluded objects by performing a second association pass using
      low-confidence detections that other trackers would discard. :doc:`L6 </lectures/lecture6/l6_index>`


.. _glossary-c:

C
=

.. glossary::

   Calibration (Extrinsic)
      The process of determining the 6-DOF transformation (rotation +
      translation) between sensors or between a sensor and the vehicle
      frame. Essential for multi-sensor fusion. :doc:`L2 </lectures/lecture2/l2_index>`

   Calibration (Intrinsic)
      The process of determining a camera's internal parameters: focal
      lengths (fx, fy), principal point (cx, cy), and distortion
      coefficients. Typically performed using checkerboard patterns. :doc:`L2 </lectures/lecture2/l2_index>`

   CARLA
      CAR Learning to Act. An open-source autonomous driving simulator
      built on Unreal Engine 4, providing realistic urban/highway
      environments, sensor simulation, and a Python API. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Chi-Square Gate
      A test that rejects a measurement whose normalised squared
      innovation exceeds a threshold taken from the chi-square
      distribution. For a two-dimensional position fix at 99 percent the
      threshold is 9.21. See Gating. :doc:`L3
      </lectures/lecture3/l3_index>`

   CIoU Loss
      Complete Intersection over Union loss. A bounding box regression
      loss used in YOLO that penalizes overlap, center distance, and
      aspect ratio simultaneously. :doc:`L4 </lectures/lecture4/l4_index>`

   Closed-Loop Evaluation
      Evaluating a system in a setting where its own decisions change what
      happens next, so errors compound as they do on a road. The only way to
      observe recovery, or a small error growing into a large one. Contrast
      :term:`Open-Loop Evaluation`. :doc:`L13 </lectures/lecture13/l13_index>`

   CNN
      Convolutional Neural Network. A class of deep neural networks that
      use convolutional layers to extract spatial features from images.
      The backbone architecture for most object detectors. :doc:`L4 </lectures/lecture4/l4_index>`

   Collision Detection
      The geometric test that determines whether a candidate path or
      trajectory intersects any obstacle (often expressed as inflated
      bounding boxes, OBBs, or Minkowski sums). Run at every node
      expansion during sampling- and graph-based planning. :doc:`L10 </lectures/lecture10/l10_index>`

   Complementarity
      The principle that different sensing modalities have strengths and
      weaknesses that offset one another, so a combination is more
      robust than any one alone. Distinct from redundancy, which
      duplicates a capability without covering its failure modes.
      :doc:`L2 </lectures/lecture2/l2_index>`

   Complementarity Principle
      The observation (Luo, 1989) that different sensor technologies have
      unique strengths and weaknesses that balance each other out, making
      multi-sensor fusion essential for robust perception. :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3 </lectures/lecture3/l3_index>`

   Concrete Scenario
      A :term:`Logical Scenario` with every parameter fixed to a value, and
      therefore the only scenario layer that can actually be executed. One
      logical scenario yields thousands of concrete ones, which is why test
      selection is a sampling problem. :doc:`L13 </lectures/lecture13/l13_index>`

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
      configuration space to simplify collision checking during planning. :doc:`L10 </lectures/lecture10/l10_index>`

   Conspicuity
      The DDT subtask of making the vehicle's presence and intent visible to
      other road users: lights, indicators, horn, gestures. A genuine gap in
      the field -- a vehicle that cannot signal its intent to a human is hard
      to share a road with -- and not covered in this course. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Cooperative Perception
      Multiple vehicles or roadside units sharing sensor data via V2X
      communication to build a collective, extended understanding of the
      driving scene beyond any single vehicle's sensor range. :doc:`L14 </lectures/lecture14/l14_index>`

   Covariance
      A measure of how much the errors in two quantities move together.
      Zero when the two are independent. :doc:`L3
      </lectures/lecture3/l3_index>`

   Covariance Matrix
      A square matrix holding variances on the diagonal and covariances
      off it. In a Kalman filter, P is the covariance of the state
      estimate. Off-diagonal terms appear on their own during
      prediction, because advancing position using velocity links the
      two. :doc:`L3 </lectures/lecture3/l3_index>`

   Coverage Interval
      The term the GUM and the VIM use in place of confidence interval,
      paired with coverage probability in place of confidence level.
      Metrology prefers these because they avoid the common misreading
      of the word confidence. :doc:`L3 </lectures/lecture3/l3_index>`

   Credible Region
      A Bayesian region that contains the true value with a stated
      probability, given the model. A Kalman filter's covariance ellipse
      is a credible region rather than a confidence interval. In two
      dimensions the 95 percent ellipse sits at 2.45 sigma, not 2 sigma.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Cross-Attention Fusion
      A deep learning fusion approach that uses transformer cross-attention
      mechanisms to learn how features from one sensor modality should
      attend to features from another (e.g., camera features attending to
      LiDAR features in BEVFusion). :doc:`L6 </lectures/lecture6/l6_index>`

   Cross-Track Error
      The lateral distance between the vehicle (typically measured at the
      front axle for Stanley, rear axle for Pure Pursuit) and the nearest
      point on the reference path. Drives the steering correction in both
      controllers. :doc:`L11 </lectures/lecture11/l11_index>`

   CTRA
      Constant Turn Rate and Acceleration. A physics-based motion prediction
      model that assumes constant yaw rate and longitudinal acceleration.
      More realistic than constant-velocity models for curving trajectories. :doc:`L9 </lectures/lecture9/l9_index>`

   C-V2X
      Cellular Vehicle-to-Everything. A 3GPP-based V2X communication
      standard (LTE-V2X, NR-V2X/5G) that leverages cellular infrastructure
      for vehicle communication. Competing with DSRC for V2X deployment. :doc:`L14 </lectures/lecture14/l14_index>`


.. _glossary-d:

D
=

.. glossary::

   DAgger
      Dataset Aggregation. An iterative imitation learning algorithm that
      addresses distribution shift by collecting new training data under
      the learner's own policy, then re-labeling with the expert's actions.
      Reduces per-step regret from :math:`O(\epsilon T^2)` (BC) to
      :math:`O(\epsilon)`. :doc:`L12 </lectures/lecture12/l12_index>`

   Data Association
      The problem of deciding which incoming measurement corresponds to
      which existing track (or that it is a new object / clutter). Solved
      by nearest-neighbour, Hungarian/GNN, JPDA, or MHT depending on the
      ambiguity tolerated. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L6 </lectures/lecture6/l6_index>`

   DDS
      Data Distribution Service. An OASIS/OMG standard for real-time
      publish-subscribe communication. The middleware layer underlying
      ROS 2, providing configurable QoS policies for message delivery. :doc:`L14 </lectures/lecture14/l14_index>`

   DDT
      Dynamic Driving Task. All real-time operational and tactical functions
      required to operate a vehicle in on-road traffic. SAE J3016 splits it
      into six subtasks: lateral control, longitudinal control, :term:`OEDR`
      detection, OEDR response, maneuver planning and :term:`Conspicuity`.
      Excludes strategic functions such as trip scheduling, destination
      choice and route selection -- so a vehicle with a flawless route
      planner and nothing else is not automated at all. :doc:`L1 </lectures/lecture1/l1_lecture>`

   DDT Fallback
      The response required when a :term:`Driving Automation Feature` can no
      longer perform the :term:`DDT`. Triggered either by a **system failure**
      or by the vehicle **reaching the edge of its ODD** -- only the first of
      which is a fault, and the second of which is more common in service. At
      Level 3 it is performed by the human :term:`Fallback-Ready User` on
      request; at Levels 4--5 the system performs it itself. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Dead Reckoning
      Estimating current position by integrating motion measurements
      (wheel odometry, IMU) from a known prior pose. Accumulates drift
      over time without external corrections. :doc:`L7 </lectures/lecture7/l7_index>`

   DeepLabv3+
      A semantic segmentation architecture (Chen et al., 2018) using atrous
      (dilated) convolutions and Atrous Spatial Pyramid Pooling (ASPP) to
      capture multi-scale context without reducing spatial resolution. :doc:`L5 </lectures/lecture5/l5_index>`

   DeepSORT
      Deep Simple Online and Realtime Tracking (Wojke et al., 2017).
      Extends SORT with a deep appearance descriptor (128-D embedding)
      for re-identification after occlusion. :doc:`L6 </lectures/lecture6/l6_index>`

   Degrees of Freedom
      How many numbers a sensor reports at once, written m. A GNSS fix
      giving x and y has m equal to 2. It selects which chi-square
      distribution the NIS should follow. :doc:`L3
      </lectures/lecture3/l3_index>`

   DETR
      DEtection TRansformer. A transformer-based object detector that
      frames detection as a set prediction problem. Uses object queries
      and bipartite matching instead of anchors and NMS. :doc:`L4 </lectures/lecture4/l4_index>`

   Diffusion-Based Planning
      Motion planning via iterative denoising of trajectories, learned
      from expert demonstrations. Models the trajectory distribution as
      a diffusion process and generates plans by reverse diffusion.
      Examples: Diffusion Planner (ICLR 2025), DiffusionDrive (CVPR 2025). :doc:`L10 </lectures/lecture10/l10_index>`

   Dijkstra
      A classical shortest-path graph search algorithm that expands nodes
      in order of accumulated cost from the source. Equivalent to A* with
      zero heuristic; preferred when no useful heuristic is available. :doc:`L8 </lectures/lecture8/l8_index>` · :doc:`L10 </lectures/lecture10/l10_index>`

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
      of behavior cloning where small errors compound over time. :doc:`L12 </lectures/lecture12/l12_index>`

   Divergence
      The failure in which a filter's reported covariance keeps
      shrinking while its true error grows. The update step shrinks P
      whether or not the update was correct, so the gain falls, new
      measurements stop affecting the estimate, and the filter reports
      high confidence in a wrong answer. :doc:`L3
      </lectures/lecture3/l3_index>`

   Domain Randomization
      Varying simulation parameters (lighting, textures, weather, sensor
      noise) during training to improve robustness and sim-to-real transfer
      of learned models. :doc:`L13 </lectures/lecture13/l13_index>`

   Doppler Effect
      The frequency shift in a reflected signal caused by the relative
      motion of the target. RADAR uses this to directly measure the
      velocity of moving objects. :doc:`L2 </lectures/lecture2/l2_index>`

   DriveTransformer
      An end-to-end autonomous driving model (ICLR 2025) that uses shared
      attention across all perception, prediction, and planning tasks,
      achieving high throughput through task-parallel processing. :doc:`L12 </lectures/lecture12/l12_index>`

   DriveVLM
      A Vision-Language-Action model for autonomous driving (Tian et al.,
      2024) that combines a vision-language reasoning model with a fast
      driving policy, producing chain-of-thought scene descriptions
      alongside action outputs. :doc:`L12 </lectures/lecture12/l12_index>`

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
      Used to score GP4. :doc:`L13 </lectures/lecture13/l13_index>`

   DSRC
      Dedicated Short-Range Communications (IEEE 802.11p). The original
      V2X communication technology operating in the 5.9 GHz band.
      Competing with C-V2X for industry adoption. :doc:`L14 </lectures/lecture14/l14_index>`

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
      sensor affect everything. :doc:`L3 </lectures/lecture3/l3_index>`

   End-to-End Driving
      An approach where a single neural network maps raw sensor input
      directly to driving actions, bypassing the traditional modular
      pipeline (perception -> planning -> control). :doc:`L12 </lectures/lecture12/l12_index>`

   EKF
      Extended Kalman Filter. A non-linear extension of the Kalman Filter
      that uses Jacobian matrices to linearize the system at each time
      step. The standard fusion filter for IMU + GNSS + wheel odometry in
      AV localization. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Expectation
      The average of a quantity taken over all possible outcomes rather
      than over a finite sample. Written with E and square brackets.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Extended Kalman Filter
      EKF. A Kalman filter for nonlinear models, which approximates them
      with straight lines at the current estimate using Jacobians. The
      standard choice for vehicle state estimation. Its failure mode is
      a feedback loop: a poor estimate gives a poor approximation, which
      gives a worse estimate. :doc:`L3 </lectures/lecture3/l3_index>`

   Extrinsic Calibration
      The rigid transform describing where one sensor sits relative to
      another, or relative to the vehicle. Six numbers. It belongs to
      the installation rather than to the sensor, and it drifts with
      vibration, temperature and knocks. :doc:`L2
      </lectures/lecture2/l2_index>`

.. _glossary-f:

F
=

.. glossary::

   Failure Boundary
      The conditions at which a system stops working, stated explicitly. A
      system with a known and reported boundary is more useful to a safety
      case than one with a high pass rate and no known limit. :doc:`L13 </lectures/lecture13/l13_index>`

   Fallback-Ready User
      The human occupant of a Level 3 vehicle who is not driving but must
      remain receptive to a request to intervene and be able to resume the
      :term:`DDT` within seconds. The role exists only at Level 3, and the
      few-seconds reacquisition of situational awareness it demands is a
      human-factors problem rather than a software one. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Filter Consistency
      Whether a filter's reported covariance matches the errors it
      actually makes. Tested with the NIS, using only quantities the
      filter already computes, so the check can run continuously on a
      vehicle without ground truth. :doc:`L3
      </lectures/lecture3/l3_index>`

   FMCW
      Frequency-Modulated Continuous Wave. The radar modulation that
      sweeps a frequency chirp and compares the returning echo against
      the outgoing sweep, which yields range and Doppler velocity
      together. :doc:`L2 </lectures/lecture2/l2_index>`

   FMEA
      Failure Mode and Effects Analysis. A systematic method for
      identifying potential failure modes in a system, assessing their
      impact, and designing mitigations (e.g., sensor redundancy). :doc:`L14 </lectures/lecture14/l14_index>`

   Focal Loss
      A modified cross-entropy loss (Lin et al., 2017) that down-weights
      easy examples to focus training on hard, misclassified cases.
      Critical for one-stage detectors dealing with extreme
      foreground/background class imbalance. :doc:`L4 </lectures/lecture4/l4_index>`

   Foundation Model
      A large neural network pre-trained on broad data at scale and
      adaptable to many downstream tasks (e.g., GPT, CLIP). In AV, used
      as VLA backbones (DriveVLM, NVIDIA Alpamayo) and as world-model
      starting points. :doc:`L12 </lectures/lecture12/l12_index>` · :doc:`L13 </lectures/lecture13/l13_index>`

   FPN
      Feature Pyramid Network. A neck architecture that fuses features
      across multiple scales via a top-down pathway with lateral
      connections, enabling detection of objects at different sizes. :doc:`L4 </lectures/lecture4/l4_index>`

   Frenet Frame
      A curvilinear coordinate system :math:`(s, d)` defined along a road
      centerline, where :math:`s` is the arc-length along the path and
      :math:`d` is the lateral offset. Simplifies trajectory planning on
      curved roads. :doc:`L11 </lectures/lecture11/l11_index>`

   FSM
      Finite State Machine. A classical approach to behavior planning using
      discrete states (lane follow, lane change, stop, yield) and
      transition rules. Simple, interpretable, but brittle for complex
      scenarios. :doc:`L9 </lectures/lecture9/l9_index>`

   Functional Scenario
      A scenario written in plain language so that humans can agree on it
      ("a vehicle cuts into my lane from the right"). The most abstract of
      the three scenario layers; refined into a :term:`Logical Scenario`. :doc:`L13 </lectures/lecture13/l13_index>`

   Fusion Architecture
      The strategy for combining data from multiple sensors. Three main
      types: early fusion (raw data), intermediate/mid-level fusion
      (features), and late fusion (detection outputs). :doc:`L3 </lectures/lecture3/l3_index>`


.. _glossary-g:

G
=

.. glossary::

   GAIA-3
      Wayve's 15-billion-parameter generative driving world model
      (December 2025) that predicts realistic future driving video
      conditioned on actions and text prompts. :doc:`L13 </lectures/lecture13/l13_index>`

   GAIA-4
      Wayve's world model announced August 2026, which added **closed-loop**
      simulation: the AI Driver's decisions change the generated future,
      rather than the scene replaying regardless. Uses a "world on rails"
      approach in which other road users keep their recorded trajectories,
      so it cannot evaluate negotiation. :doc:`L13 </lectures/lecture13/l13_index>`

   Gating
      Rejecting a measurement that disagrees with the current estimate
      by more than a threshold. It is the answer to the GNSS multipath
      problem raised in L2. Its own failure mode: once an estimate has
      drifted, the gate rejects the correct measurements that would have
      corrected it. :doc:`L3 </lectures/lecture3/l3_index>`

   Geofence
      A boundary in the physical world, encoded in software, outside which a
      :term:`Driving Automation Feature` will not operate. One common way of
      expressing the geographic component of an :term:`ODD`. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Global Nearest Neighbor
      GNN. Data association that solves a whole frame at once, choosing
      the set of pairings with the lowest total cost, usually with the
      Hungarian algorithm. Removes the order dependence that makes plain
      nearest-neighbour association unreliable. :doc:`L3
      </lectures/lecture3/l3_index>`

   GNN
      Graph Neural Network. A neural network operating on graph-structured
      data. Used in trajectory prediction to model interactions between
      agents, where nodes represent agents and edges represent
      relationships. :doc:`L9 </lectures/lecture9/l9_index>`

   GNSS
      Global Navigation Satellite System. Provides absolute position
      (latitude, longitude, altitude). Includes GPS (US), GLONASS
      (Russia), Galileo (EU), BeiDou (China). :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Ground Truth
      The true value of a quantity. Available in simulation and never
      available on a real vehicle. Used to check whether a filter's
      reported uncertainty matches the error it is actually making.
      :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

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
      severity, exposure, and controllability, and assigning ASIL levels. :doc:`L14 </lectures/lecture14/l14_index>`

   Hardware-in-the-Loop (HIL)
      A test level in which real ECUs run the software with real timing while
      the world remains simulated. Catches latency, scheduling and resource
      limits that :term:`Software-in-the-Loop (SIL)` cannot. :doc:`L13 </lectures/lecture13/l13_index>`

   HD Map
      High-Definition map with centimeter-accurate road geometry, lane
      markings, traffic signs, and semantic annotations. Used for precise
      localization by matching live sensor data against the map. :doc:`L7 </lectures/lecture7/l7_index>` · :doc:`L8 </lectures/lecture8/l8_index>`

   Head (Detection)
      The final component of an object detection architecture that
      produces bounding box coordinates and class predictions. Can be
      anchor-based (YOLO v3--v7) or anchor-free (YOLOv8+, DETR). :doc:`L4 </lectures/lecture4/l4_index>`

   HOTA
      Higher Order Tracking Accuracy. A tracking evaluation metric that
      balances detection quality and association quality equally via
      their geometric mean, addressing biases in MOTA and IDF1. :doc:`L6 </lectures/lecture6/l6_index>`

   Hungarian Algorithm
      An optimization algorithm that finds the minimum-cost one-to-one
      assignment between two sets. Used by DETR for bipartite matching
      between predictions and ground truth, and by SORT/DeepSORT for
      association between predicted tracks and new detections. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L6 </lectures/lecture6/l6_index>`


.. _glossary-i:

I
=

.. glossary::

   ICP
      Iterative Closest Point. An algorithm for aligning two point clouds
      by iteratively finding closest-point correspondences and minimizing
      the alignment error. Core algorithm for scan matching in SLAM and
      LiDAR odometry. :doc:`L7 </lectures/lecture7/l7_index>`

   IDF1
      Identity F1 Score. A tracking evaluation metric computed as the F1
      score of correct identity assignments. Emphasizes consistent ID
      maintenance over raw detection accuracy. :doc:`L6 </lectures/lecture6/l6_index>`

   IMU
      Inertial Measurement Unit. Measures linear acceleration
      (accelerometers) and angular velocity (gyroscopes) at high
      frequency (>100 Hz). Suffers from drift over time. :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Innovation
      The measurement minus the measurement the filter predicted,
      written with the Greek letter nu. The only genuinely new
      information in a filter cycle, and the quantity that consistency
      checks monitor. Many textbooks write it as y. :doc:`L3
      </lectures/lecture3/l3_index>`

   Innovation Covariance
      How large the filter expected the innovation to be, written S.
      Used by the Kalman gain, the NIS and the Mahalanobis distance.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Instance Segmentation
      A perception task that assigns each object a unique ID and
      pixel-level mask, distinguishing individual instances of the same
      class (e.g., car #1 vs. car #2). :doc:`L5 </lectures/lecture5/l5_index>`

   Intermediate Fusion
      Combining learned features from each sensor. The network can learn
      which sensor to trust in which conditions, at the cost of needing
      training data with every modality present, and of being hard to
      interpret or certify. :doc:`L3 </lectures/lecture3/l3_index>`

   Intrinsic Calibration
      The parameters describing how a camera turns an incoming ray of
      light into a pixel: focal lengths, principal point and distortion
      coefficients. They belong to the camera and lens, so they travel
      with it and are far more stable than extrinsics. :doc:`L2
      </lectures/lecture2/l2_index>`

   Inverse-Variance Weighting
      Combining independent estimates with weights proportional to one
      over the variance. The precisions add, so the combined uncertainty
      is smaller than either input. Halving a sensor's sigma multiplies
      its weight by four. :doc:`L3 </lectures/lecture3/l3_index>`

   IoU
      Intersection over Union. The ratio of the overlap area to the
      union area of a predicted and ground truth bounding box. Used as
      the primary metric for evaluating detection localization. :doc:`L4 </lectures/lecture4/l4_index>`

   ISO 26262
      International standard for functional safety of road vehicle
      electrical and electronic systems. Defines ASIL levels to classify
      risk severity. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   ISO 21448 (SOTIF)
      Safety of the Intended Functionality. Addresses safety hazards that
      occur without a system failure (e.g., sensor limitations). A
      critical complement to ISO 26262. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`


   ISO 34502
      *Road vehicles — Test scenarios for automated driving systems —
      Scenario based safety evaluation framework* (2022). Part of the ISO
      34500 series: 34501 vocabulary, 34502 evaluation framework, 34503 ODD
      taxonomy, 34504 scenario categorization, 34505 test case generation. :doc:`L13 </lectures/lecture13/l13_index>`

.. _glossary-j:

J
=

.. glossary::

   JPDA
      Joint Probabilistic Data Association. A probabilistic data
      association method for multi-target tracking in clutter that
      considers all possible measurement-to-track assignments weighted
      by their probabilities. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L6 </lectures/lecture6/l6_index>`


.. _glossary-k:

K
=

.. glossary::

   Kalman Filter
      An optimal recursive estimator for linear systems with Gaussian
      noise. Uses a predict-update cycle to fuse noisy sensor measurements
      over time. Foundation of IMU+GNSS fusion and the state-update step
      inside SORT and DeepSORT. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L6 </lectures/lecture6/l6_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Kalman Gain
      The blending factor in the Kalman Filter that determines how much
      weight to give to the new measurement vs. the prediction. High
      trust in sensor = high gain; high trust in prediction = low gain. :doc:`L3 </lectures/lecture3/l3_index>`


.. _glossary-l:

L
=

.. glossary::

   Lanelet2
      An open lane-graph map format (Poggenhans et al., 2018) widely used
      by Autoware and many research stacks. Represents drivable lanes as
      typed line strings with explicit topological connectivity. :doc:`L8 </lectures/lecture8/l8_index>`

   Late Fusion
      Combining finished per-sensor results such as tracks, object lists
      or pose estimates. Modular, testable and robust to a failed
      sensor, but information is discarded before the combination
      happens. This is what GP3 uses. :doc:`L3
      </lectures/lecture3/l3_index>`

   Lattice Planner
      A motion planning approach that performs graph search on a
      pre-computed state lattice of kinematically feasible motion
      primitives. Combines the completeness of graph search with
      kinematic feasibility. :doc:`L10 </lectures/lecture10/l10_index>`

   LiDAR
      Light Detection and Ranging. Uses laser pulses and time-of-flight
      to measure distances, producing 3D point clouds. Key specs: range,
      points per second, accuracy, beam count. :doc:`L2 </lectures/lecture2/l2_index>`

   LiDAR Odometry
      Estimating ego-motion by matching consecutive LiDAR scans using
      algorithms like ICP or feature-based methods (LOAM). More robust
      than visual odometry in low-light and textureless environments. :doc:`L7 </lectures/lecture7/l7_index>`

   Lift-Splat-Shoot (LSS)
      A foundational camera-to-BEV projection method (Philion & Fidler,
      NeurIPS 2020) that predicts per-pixel depth distributions (Lift),
      projects features into a voxel grid (Splat), and collapses to BEV
      (Shoot). Fully differentiable end-to-end. :doc:`L5 </lectures/lecture5/l5_index>`

   LOAM
      LiDAR Odometry and Mapping. A foundational LiDAR SLAM system that
      separates high-frequency odometry (edge and planar feature matching)
      from low-frequency mapping for real-time operation. :doc:`L7 </lectures/lecture7/l7_index>`

   Logical Scenario
      A :term:`Functional Scenario` with its parameters named and given
      *ranges* (gap 5–30 m, closing speed 0–15 m/s). Still not runnable;
      fixing the values produces a :term:`Concrete Scenario`. :doc:`L13 </lectures/lecture13/l13_index>`

   Long-Tail Scenarios
      Rare but safety-critical driving events (e.g., a mattress on the
      highway, a child running into the road) that are underrepresented
      in training data. The primary data challenge in AV development. :doc:`L13 </lectures/lecture13/l13_index>` · :doc:`L14 </lectures/lecture14/l14_index>`

   Loop Closure
      Detection of a previously visited location during SLAM, used to
      correct accumulated drift by adding a constraint in the pose graph.
      Methods include scan context, visual bag-of-words, and neural
      descriptors. :doc:`L7 </lectures/lecture7/l7_index>`


.. _glossary-m:

M
=

.. glossary::

   Mahalanobis Distance
      A distance metric that accounts for the covariance (uncertainty)
      of a distribution. Used in data association to determine whether a
      measurement is statistically consistent with a predicted track state. :doc:`L3 </lectures/lecture3/l3_index>`

   mAP
      Mean Average Precision. The primary metric for evaluating object
      detectors. mAP@0.5 uses a single IoU threshold; mAP@0.5:0.95
      averages across thresholds for stricter evaluation. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>`

   Mask R-CNN
      An instance segmentation model (He et al., 2017) that extends Faster
      R-CNN with a mask head predicting a binary segmentation mask for each
      detected bounding box, enabling pixel-level object delineation. :doc:`L5 </lectures/lecture5/l5_index>`

   MCL
      Monte Carlo Localization. A particle filter-based localization
      algorithm that represents the robot's belief as a set of weighted
      samples. AMCL (Adaptive MCL) dynamically adjusts particle count.
      Standard localization algorithm in ROS. :doc:`L7 </lectures/lecture7/l7_index>`

   Mean
      The average of a set of readings, written with the Greek letter
      mu. :doc:`L3 </lectures/lecture3/l3_index>`

   Measurement Noise
      The random error in a sensor reading, with covariance R. Usually
      measurable, by pointing the sensor at a known target and examining
      the spread. :doc:`L3 </lectures/lecture3/l3_index>`

   MHT
      Multiple Hypothesis Tracking. A data association method that
      maintains a tree of hypotheses for measurement-to-track assignments,
      deferring hard decisions to resolve ambiguity over time. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L6 </lectures/lecture6/l6_index>`

   Modality
      A kind of sensing rather than a piece of hardware. Two cameras are
      one modality; a camera and a radar are two. Complementarity is a
      claim about modalities, never about counts. :doc:`L2
      </lectures/lecture2/l2_index>`

   M-of-N
      The rule that promotes a tentative track to confirmed, requiring M
      detections within N frames. It stops clutter from being reported
      as a real object, at the cost of a short delay before a genuine
      object is confirmed. :doc:`L3 </lectures/lecture3/l3_index>`

   MOTA
      Multi-Object Tracking Accuracy. A tracking metric computed as
      :math:`1 - (FN + FP + IDSW) / GT`, penalizing false negatives,
      false positives, and identity switches. Range: :math:`(-\infty, 1]`. :doc:`L6 </lectures/lecture6/l6_index>`

   MOTP
      Multi-Object Tracking Precision. The average overlap (IoU) between
      true positives and their assigned ground-truth boxes. Complements
      MOTA by measuring localisation quality independently of identity
      switches. :doc:`L6 </lectures/lecture6/l6_index>`

   MPC
      Model Predictive Control. A receding-horizon optimization-based
      controller that solves a finite-horizon optimal control problem at
      each time step, applying only the first control action. Dominant
      controller in production AV systems. :doc:`L11 </lectures/lecture11/l11_index>`

   MRC
      Minimal Risk Condition. The stable, low-risk state a vehicle reaches
      when a trip cannot be completed -- the *where you end up* that follows
      the :term:`DDT Fallback`'s *who takes over*. Note that it is **not**
      triggered only by failures: leaving the ODD reaches it too.

      **An MRC is a design artifact.** Somebody decided in advance what
      "safe" means and validated it against a list of situations they thought
      of; if reality is not on the list, the vehicle still follows the list.
      Every candidate hides an assumption -- stopping in place assumes traffic
      behind can react, pulling over assumes a shoulder exists and that
      nothing is trapped underneath. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   Multi-Modal Prediction
      A trajectory prediction output that represents several plausible
      futures simultaneously (typically as :math:`K` weighted trajectory
      modes), capturing the inherent uncertainty in other agents'
      intentions. :doc:`L9 </lectures/lecture9/l9_index>`

   Multi-Object Tracking (MOT)
      The task of maintaining consistent identity for detected objects
      across consecutive frames. Methods: SORT, DeepSORT, ByteTrack,
      transformer-based MOT. :doc:`L6 </lectures/lecture6/l6_index>`

   Multipath
      A GNSS error in which the signal arrives by a reflected path
      rather than directly, so the receiver places the vehicle several
      metres from its true position. The fix arrives on time and looks
      entirely normal, which makes it more dangerous than a lost fix.
      :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

.. _glossary-n:

N
=

.. glossary::

   Neck
      The multi-scale feature fusion component of a detection
      architecture, positioned between the backbone and head. Examples:
      FPN, PAN, BiFPN. :doc:`L4 </lectures/lecture4/l4_index>`

   NDS
      nuScenes Detection Score. A composite ranking metric for 3D object
      detection on nuScenes, combining mAP with five true-positive error
      metrics (translation, scale, orientation, velocity, attribute). :doc:`L5 </lectures/lecture5/l5_index>`

   NDT
      Normal Distributions Transform. A point cloud registration method
      that represents clouds as a grid of Gaussian distributions.
      Used in Autoware for LiDAR-based localization. Faster than ICP
      for large-scale matching. :doc:`L7 </lectures/lecture7/l7_index>`

   NIS
      Normalised Innovation Squared. The innovation weighted by the
      inverse of its expected covariance. It should follow a chi-square
      distribution if the filter is consistent. Persistently above the
      expected range means the filter is overconfident. :doc:`L3
      </lectures/lecture3/l3_index>`

   NMS
      Non-Maximum Suppression. A post-processing step that removes
      duplicate detections by suppressing overlapping bounding boxes
      with lower confidence. Not needed in DETR. :doc:`L4 </lectures/lecture4/l4_index>`

   Noise
      Random error that scatters readings around a centre and averages
      away as more readings are taken. Described by variance. Contrast
      with bias, which does not average away. :doc:`L3
      </lectures/lecture3/l3_index>`

   Nonholonomic Constraint
      A motion constraint that limits achievable velocities but not the
      configuration space itself. A car cannot move sideways instantaneously
      (no lateral velocity in the body frame) -- planners must respect this
      when generating paths. :doc:`L10 </lectures/lecture10/l10_index>`

   nuScenes
      A widely used AV benchmark dataset (Caesar et al., 2020) with
      synchronized 6-camera, 5-radar, 1-LiDAR, IMU, and GPS data over
      1000 driving scenes. Standard evaluation for BEV detection and
      tracking; uses the NDS composite score. :doc:`L5 </lectures/lecture5/l5_index>`

   NVIDIA Cosmos
      NVIDIA's family of world foundation models for physical AI,
      designed to generate realistic driving video and enable
      simulation-based AV training and evaluation. :doc:`L13 </lectures/lecture13/l13_index>`


.. _glossary-o:

O
=

.. glossary::

   Object Query
      In DETR, a learned embedding that is input to the transformer
      decoder. Each query attends to the encoded image features via
      cross-attention and specializes in detecting one object. :doc:`L4 </lectures/lecture4/l4_index>`

   ODD
      Operational Design Domain. The specific operating conditions
      (geographic, environmental, traffic) under which an ADS is designed
      to function safely. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Occupancy Network (3D)
      A perception architecture that predicts the semantic state of every
      voxel in a 3D volume around the vehicle, capturing arbitrary geometry
      beyond what bounding boxes can represent. Key methods: MonoScene,
      TPVFormer, Occ3D. :doc:`L5 </lectures/lecture5/l5_index>`

   ODD Coverage
      The fraction of the claimed :term:`ODD` that a test campaign actually
      exercised. The coverage figure a safety case wants, and only ever as
      good as the ODD it is measured against. Not mileage, and not a pass
      rate. :doc:`L13 </lectures/lecture13/l13_index>`

   OEDR
      Object and Event Detection and Response. The :term:`DDT` subtask of
      monitoring the driving environment -- detecting and classifying objects
      and events and deciding on a response -- and then executing that
      response. Detection is covered in L4--L6; response in L10 and L11. :doc:`L1 </lectures/lecture1/l1_lecture>`

   OES
      Operating Envelope Specification. A formal, machine-readable format
      proposed by NIST for precisely defining an ADS's ODD. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Open-Loop Evaluation
      Replaying a fixed recording past a system, so its decisions cannot
      change what happens next. Correct for perception regression testing,
      and unable to evaluate driving: brake in a replay and the recorded
      world carries on regardless. Contrast
      :term:`Closed-Loop Evaluation`. :doc:`L13 </lectures/lecture13/l13_index>`

   OpenDRIVE
      An ASAM open standard for describing road networks (geometry,
      lanes, signals, junctions) in XML. Widely used as an interchange
      format between map providers, simulators (including CARLA), and
      planning stacks. :doc:`L8 </lectures/lecture8/l8_index>`


   OpenSCENARIO
      An ASAM interchange format describing *what happens* on a road network
      — actors, manoeuvres and triggers — as a companion to
      :term:`OpenDRIVE`, which describes the road itself. Makes a scenario
      portable between simulators. :doc:`L13 </lectures/lecture13/l13_index>`

.. _glossary-p:

P
=

.. glossary::

   PAN
      Path Aggregation Network. A neck architecture that adds a bottom-up
      pathway to FPN, improving information flow for accurate localization.
      Used in YOLO v4+. :doc:`L4 </lectures/lecture4/l4_index>`

   Panoptic Segmentation
      A perception task that combines semantic segmentation (labeling
      "stuff" like road, sky) with instance segmentation (identifying
      individual "things" like cars, pedestrians). :doc:`L5 </lectures/lecture5/l5_index>`

   Particle Filter
      A non-parametric filter that approximates probability distributions
      using a set of weighted random samples (particles). Can handle
      arbitrary non-linear and non-Gaussian systems. :doc:`L3 </lectures/lecture3/l3_index>` · :doc:`L7 </lectures/lecture7/l7_index>`

   Perception
      The process by which an autonomous system transforms unstructured
      sensor data into a structured, semantic understanding of the
      surrounding environment. :doc:`L4 </lectures/lecture4/l4_index>` · :doc:`L5 </lectures/lecture5/l5_index>` · :doc:`L6 </lectures/lecture6/l6_index>`

   PID Controller
      Proportional-Integral-Derivative controller. A classical feedback
      controller used for longitudinal speed control in AVs. The three
      terms correct present error (P), accumulated past error (I), and
      predicted future error (D). :doc:`L11 </lectures/lecture11/l11_index>`

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

   Pose Graph Optimization
      The SLAM backend formulation that represents the robot trajectory
      as a graph of poses (nodes) and relative constraints (edges), then
      optimizes all poses jointly to minimize constraint errors. :doc:`L7 </lectures/lecture7/l7_index>`

   Precision
      The fraction of detections that are correct: TP / (TP + FP).
      High precision means few false positives. :doc:`L4 </lectures/lecture4/l4_index>`

   PRM
      Probabilistic Road Map. A multi-query sampling-based planner that
      pre-computes a graph of collision-free configurations connected by
      feasible paths, then searches this graph for start-to-goal queries. :doc:`L10 </lectures/lecture10/l10_index>`

   Process Noise
      How wrong the motion model is, with covariance Q. It cannot be
      measured the way measurement noise can, because it describes the
      inadequacy of your own model. It is tuned, and it is the usual
      cause of an overconfident filter. :doc:`L3
      </lectures/lecture3/l3_index>`

   Pure Pursuit
      A geometric path-following controller that steers the vehicle toward
      a lookahead point on the reference path. The steering angle is
      computed from the curvature of the arc connecting the rear axle to
      the lookahead point. :doc:`L11 </lectures/lecture11/l11_index>`


.. _glossary-q:

Q
=

.. glossary::

   QoS
      Quality of Service. Configurable DDS policies governing message
      delivery in ROS 2, including reliability (best-effort vs. reliable),
      durability (transient-local vs. volatile), deadline, and lifespan.
      Critical for tuning real-time AV communication. :doc:`L14 </lectures/lecture14/l14_index>`

   Quintic Polynomial Trajectory
      A 5th-degree polynomial trajectory that matches position, velocity,
      and acceleration boundary conditions at start and end points,
      producing smooth, jerk-minimized motion profiles for comfort. :doc:`L11 </lectures/lecture11/l11_index>`


.. _glossary-r:

R
=

.. glossary::

   RADAR
      Radio Detection and Ranging. Uses radio waves to detect objects,
      measure distance, and directly measure velocity via the Doppler
      effect. Operates in all weather conditions. Standard automotive
      frequency: 77 GHz. :doc:`L2 </lectures/lecture2/l2_index>`

   Redundancy
      Duplicating a capability. It protects against a component failing
      but not against a shared environmental failure. Two identical
      forward cameras are redundant, and are blinded by the same sun
      glare at the same instant. :doc:`L2 </lectures/lecture2/l2_index>`

   Re-simulation
      Replaying recorded drives against a new software build, also called log
      replay. The regression test of AV development: it proves you have not
      broken what previously worked. Being :term:`Open-Loop Evaluation`, it
      is not by itself a validation of driving ability. :doc:`L13 </lectures/lecture13/l13_index>`

   Recall
      The fraction of real objects that the detector successfully found:
      TP / (TP + FN). High recall means few missed detections. :doc:`L4 </lectures/lecture4/l4_index>`

   Reinforcement Learning (RL)
      Learning by optimizing a reward function through trial and error.
      Used in AV systems for planner fine-tuning (e.g., NVIDIA's
      end-to-end stack) and scenario-based policy improvement. :doc:`L12 </lectures/lecture12/l12_index>`

   Remote Assistance
      A remote human **advising** an automated vehicle -- for example,
      confirming that it may proceed around an obstruction -- without taking
      control of the driving task. Does not change the vehicle's level. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Remote Driving
      A remote human **taking the controls** of a vehicle. This is a distinct
      mode of operation, not a :term:`DDT Fallback`, and its availability
      does not change the level of the automated feature. Contrast
      :term:`Remote Assistance`. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Reprojection Error
      The distance (in pixels) between a known 3D point projected onto
      the image using calibrated parameters and its actual observed
      position. Used to validate calibration quality; should be < 2 px. :doc:`L2 </lectures/lecture2/l2_index>`

   ResNet
      Residual Network. A CNN architecture (He et al., 2016) that
      introduced skip connections, enabling training of very deep
      networks (50--152 layers) without degradation. :doc:`L4 </lectures/lecture4/l4_index>`

   Rolling Shutter
      A camera readout mode where image rows are exposed sequentially
      rather than simultaneously. Produces "jello"-like distortion of
      fast-moving objects and complicates calibration in dynamic scenes;
      global-shutter sensors avoid this at higher cost. :doc:`L2 </lectures/lecture2/l2_index>`

   ROS 2
      Robot Operating System 2. An open-source middleware framework for
      building robotic systems, built on DDS for real-time communication.
      Industry standard for AV development. Used throughout ENPM818Z for
      the ``ads_pipeline`` package. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   Route Completion
      The percentage of a route's distance an agent covered. One of the two
      factors in the :term:`Driving Score`; driving off-road reduces it
      rather than incurring a separate penalty. GP4 requires at least
      70%. :doc:`L13 </lectures/lecture13/l13_index>`

   RRT
      Rapidly-Exploring Random Tree. A sampling-based motion planning
      algorithm that incrementally builds a tree of feasible configurations
      by random sampling. RRT* is its asymptotically optimal variant. :doc:`L10 </lectures/lecture10/l10_index>`

   RT-DETR
      Real-Time DETR. A transformer-based detector with an efficient
      hybrid encoder that achieves real-time speed competitive with YOLO
      while maintaining the NMS-free architecture. :doc:`L4 </lectures/lecture4/l4_index>`

   RTK-GPS
      Real-Time Kinematic GPS. A GNSS technique using carrier-phase
      measurements and a nearby base station to achieve centimeter-level
      positioning accuracy. Essential for high-precision AV localization. :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L7 </lectures/lecture7/l7_index>`


.. _glossary-s:

S
=

.. glossary::

   SAE J3016
      The Society of Automotive Engineers standard that defines six levels
      of driving automation (Level 0--5), the industry-standard
      classification system. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Scale Ambiguity
      A single image cannot determine absolute size or distance, because
      a small near object and a large far one project onto identical
      pixels. Scale has to come from elsewhere: camera height, known
      object sizes, ego-motion, or another sensor. :doc:`L2
      </lectures/lecture2/l2_index>`

   Scan Matching
      Aligning a new LiDAR scan to a previous scan or map by finding the
      rigid transformation that minimizes inter-point distance. Algorithms
      include ICP, NDT, and feature-based variants -- the workhorse of
      LiDAR localization and SLAM. :doc:`L7 </lectures/lecture7/l7_index>`

   Safety Case
      A written argument that a system is acceptably safe in a given context,
      in three parts: **claims** (what the system will not do), **arguments**
      (why that is believed) and **evidence** (results supporting each
      argument). A folder of test results is not a safety case, because it
      never states what the results were supposed to prove. Assembled in
      Stage 5 of the concept-to-road pipeline and read there, for the first
      time, by someone outside the developer. :doc:`L1 </lectures/lecture1/l1_lecture>`

   Scenario-Based Testing
      Validating an ADS against a deliberately enumerated set of situations
      rather than against distance driven, which is infeasible: demonstrating
      human-equivalent safety statistically would take hundreds of millions
      of miles. Trades an impossible sampling problem for a hard
      completeness argument. :doc:`L13 </lectures/lecture13/l13_index>`

   Semantic Segmentation
      A perception task that assigns a class label to every pixel in an
      image (e.g., road, sidewalk, vehicle) without distinguishing
      individual instances. :doc:`L5 </lectures/lecture5/l5_index>`

   Sensor Fusion
      Combining measurements from several sensors into a single estimate
      that is better than any one sensor could provide alone. :doc:`L2
      </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

   Sigma Points
      The set of sample points a UKF chooses so that they reproduce the
      current mean and covariance exactly. They are pushed through the
      true nonlinear function, which avoids computing any Jacobian.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Sim-to-Real Gap
      The distributional mismatch between simulation-generated data and
      real-world sensor data. A fundamental challenge for training AV
      models in simulation. Mitigations include domain randomization,
      neural rendering, and fine-tuning on real data. :doc:`L13 </lectures/lecture13/l13_index>`

   SLAM
      Simultaneous Localization and Mapping. The problem of building a
      map of an unknown environment while simultaneously tracking the
      agent's pose within it. Comprises a frontend (scan matching,
      feature extraction) and backend (pose graph optimization, loop
      closure). :doc:`L7 </lectures/lecture7/l7_index>`

   Software-in-the-Loop (SIL)
      A test level in which the real software runs against simulated sensors
      and vehicle dynamics. This is CARLA, and the level every project in
      this course occupies. Misses timing, hardware faults and real sensor
      noise. :doc:`L13 </lectures/lecture13/l13_index>`

   SORT
      Simple Online and Realtime Tracking (Bewley et al., 2016). A
      minimal, efficient multi-object tracker using a Kalman filter for
      state prediction and the Hungarian algorithm for IoU-based data
      association. :doc:`L6 </lectures/lecture6/l6_index>`

   SOTIF
      See :term:`ISO 21448 (SOTIF)`. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   Standard Deviation
      The square root of the variance, written with the Greek letter
      sigma, expressed in the same units as the measurement. The usual
      way to quote an uncertainty. :doc:`L3
      </lectures/lecture3/l3_index>`

   Stanley Controller
      A lateral path-following controller (developed for the DARPA Grand
      Challenge) that computes steering based on both heading error and
      cross-track error measured at the front axle. More aggressive
      correction than Pure Pursuit at high cross-track errors. :doc:`L11 </lectures/lecture11/l11_index>`

   State Vector
      The list of quantities a filter estimates, written in bold. It
      includes quantities no sensor reports directly, such as velocity,
      because the motion model needs them and the filter can infer them.
      :doc:`L3 </lectures/lecture3/l3_index>`

   Stereo Vision
      Depth estimation using two cameras separated by a known baseline.
      Computes depth from the disparity between left and right images. :doc:`L2 </lectures/lecture2/l2_index>`

   Systematic Error
      See Bias. :doc:`L3 </lectures/lecture3/l3_index>`

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
      dozens at the bottom. :doc:`L13 </lectures/lecture13/l13_index>`

   Time of Flight
      Measuring distance by timing how long a pulse takes to travel out
      and back. For LiDAR the range is c times t divided by 2, so 2 cm
      of range accuracy requires about 133 picoseconds of timing
      precision. :doc:`L2 </lectures/lecture2/l2_index>`

   Time-of-Flight (ToF)
      The operating principle of LiDAR. Measures the round-trip time of a
      laser pulse to compute distance: ``distance = (c x dt) / 2``. :doc:`L2 </lectures/lecture2/l2_index>`

   Track Lifecycle
      The states a track passes through: tentative, confirmed, coasting
      and deleted. Track identity must not depend on classification,
      which is the architectural lesson of the Tempe crash. :doc:`L3
      </lectures/lecture3/l3_index>`

   Tracking-by-Detection
      The dominant MOT paradigm: at each frame, run an object detector,
      then associate the new detections with existing tracks (via
      KF prediction + Hungarian / cosine appearance matching). Decouples
      the detector and the tracker. :doc:`L6 </lectures/lecture6/l6_index>`

   Transfer Learning
      Starting with a model pre-trained on a large dataset (e.g., COCO)
      and fine-tuning it on a smaller target dataset. Reduces training
      time and data requirements. :doc:`L4 </lectures/lecture4/l4_index>`

   Trajectory Prediction
      Forecasting the future positions and states of other traffic agents
      (vehicles, pedestrians, cyclists) over a prediction horizon.
      Methods range from physics-based (CTRA) to transformer-based
      models generating multi-modal trajectory distributions. :doc:`L9 </lectures/lecture9/l9_index>`

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


.. _glossary-u:

U
=

.. glossary::

   UKF
      Unscented Kalman Filter. A non-linear filter that uses
      deterministic "sigma points" passed through the true non-linear
      function, avoiding the need for Jacobian matrices. :doc:`L3 </lectures/lecture3/l3_index>`

   Uncertainty
      A number attached to an estimate saying how far the truth could
      plausibly be from it. Formally, VIM clause 2.26 defines
      measurement uncertainty as a non-negative parameter characterising
      the spread of values that could reasonably be attributed to the
      quantity being measured. Usually expressed as a standard
      deviation. :doc:`L3 </lectures/lecture3/l3_index>`

   U-Net
      An encoder-decoder segmentation architecture (Ronneberger et al.,
      2015) with skip connections that concatenate encoder features with
      decoder features at matching resolutions, preserving fine spatial
      detail for pixel-precise segmentation. :doc:`L5 </lectures/lecture5/l5_index>`

   UNECE GTR
      United Nations Economic Commission for Europe Global Technical
      Regulation. Work toward a harmonized, **safety-case-based**
      international framework for ADS is underway at UNECE. Check its current
      status before citing it. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L14 </lectures/lecture14/l14_index>`

   UNECE R157
      UN Regulation No. 157, covering the approval of Automated Lane Keeping
      Systems. The regulation that made the first Level 3 highway deployments
      possible under EU-style type approval. :doc:`L1 </lectures/lecture1/l1_lecture>`

   UniAD
      Unified Autonomous Driving (CVPR 2023 Best Paper). A landmark
      end-to-end architecture that jointly performs perception, prediction,
      and planning through a unified transformer framework with
      planning-oriented task design. :doc:`L12 </lectures/lecture12/l12_index>`

   Unscented Kalman Filter
      UKF. A filter for nonlinear models that propagates sigma points
      through the true function instead of linearising it. It needs no
      Jacobians, which removes a class of silent bugs, and it is more
      accurate than the EKF when the covariance is wide. :doc:`L3
      </lectures/lecture3/l3_index>`

   Urban Canyon
      A street lined with tall buildings, where GNSS suffers both
      blockage, which is the honest failure, and multipath, which is
      not. :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

.. _glossary-v:

V
=

.. glossary::

   Variance
      How spread out a set of measurements is: the average of the
      squared distances from the mean. Squaring removes the sign and
      weights large errors more heavily. The result is in squared units,
      so the square root is usually quoted instead. :doc:`L3
      </lectures/lecture3/l3_index>`

   VIM
      International Vocabulary of Metrology, JCGM 200:2012. The source
      of this course's formal definitions of calibration and of
      measurement uncertainty. :doc:`L2 </lectures/lecture2/l2_index>` ·
      :doc:`L3 </lectures/lecture3/l3_index>`

   V-Model
      The ISO 26262 development lifecycle where each design stage (left
      side) is paired with a corresponding verification/test stage (right
      side), ensuring systematic validation from unit to system level. :doc:`L14 </lectures/lecture14/l14_index>`

   V2X
      Vehicle-to-Everything communication. Includes V2V (vehicle-to-
      vehicle), V2I (vehicle-to-infrastructure), and V2P (vehicle-to-
      pedestrian). Enables cooperative perception and situational
      awareness. :doc:`L14 </lectures/lecture14/l14_index>`

   Vehicle-in-the-Loop (VIL)
      A test level in which a real vehicle on a rig or test pad is fed
      synthetic objects, combining real dynamics and actuation with injected
      traffic that cannot cause harm. :doc:`L13 </lectures/lecture13/l13_index>`

   Vista
      A generalizable driving world model (NeurIPS 2024) that learns to
      predict diverse future video from a small amount of driving data,
      enabling synthetic scenario generation for evaluation. :doc:`L13 </lectures/lecture13/l13_index>`

   ViT
      Vision Transformer. A transformer architecture (Dosovitskiy et al.,
      2021) that splits images into patches and processes them as a
      sequence, applying self-attention for image classification. :doc:`L4 </lectures/lecture4/l4_index>`

   Visual Odometry
      Estimating camera ego-motion by tracking visual features across
      consecutive frames. Methods include feature-based (ORB-SLAM) and
      direct (DSO) approaches. Provides drift-prone but high-frequency
      relative pose updates. :doc:`L7 </lectures/lecture7/l7_index>`

   VLA Model
      Vision-Language-Action model. A multimodal architecture that
      combines visual perception, language reasoning (chain-of-thought),
      and action prediction for autonomous driving. Examples: DriveVLM,
      NVIDIA Alpamayo. :doc:`L12 </lectures/lecture12/l12_index>`

   Voxel
      A volumetric pixel -- a discrete cell in a 3D grid. Used to
      represent point clouds (voxelization), BEV features, and 3D
      occupancy maps. Voxel size determines the trade-off between
      resolution and computational cost. :doc:`L5 </lectures/lecture5/l5_index>`

   VQ-VAE
      Vector Quantized Variational Autoencoder. A generative model that
      encodes inputs into discrete codebook tokens. Used in world models
      as a visual tokenizer to compress video frames into sequences of
      discrete tokens for autoregressive prediction. :doc:`L13 </lectures/lecture13/l13_index>`


.. _glossary-w:

W
=

.. glossary::

   Waypoint
      In CARLA, a discrete point on the road network containing lane
      information, speed limits, and connectivity to other waypoints.
      Used for path planning and navigation. :doc:`L1 </lectures/lecture1/l1_lecture>` · :doc:`L8 </lectures/lecture8/l8_index>`

   White Noise
      Noise whose errors are unrelated from one moment to the next, with
      no drift or slow wander. Assumed by the Kalman filter. A sensor
      whose error wanders slowly breaks the assumption, and the filter
      will trust it too much. :doc:`L3 </lectures/lecture3/l3_index>`

   World Model
      A learned model that predicts future scene states (typically video
      frames) conditioned on actions and current observations. Acts as
      a data-driven simulator for training, evaluation, and imagination-
      based planning. Examples: GAIA-3, NVIDIA Cosmos, Vista. :doc:`L13 </lectures/lecture13/l13_index>`


.. _glossary-y:

Y
=

.. glossary::

   YOLO
      You Only Look Once. A family of single-stage object detectors that
      predict all bounding boxes and class probabilities in a single
      forward pass. Evolution: v1 (2015) to v11 (2024). :doc:`L4 </lectures/lecture4/l4_index>`


.. _glossary-z:

Z
=

.. glossary::

   Zero-Doppler Filtering
      Discarding radar returns whose Doppler shift matches the
      stationary world, so that the vehicle does not brake for manhole
      covers and sign gantries. A stopped vehicle in your lane fails
      exactly the same test, which is implicated in real crashes.
      :doc:`L2 </lectures/lecture2/l2_index>` · :doc:`L3
      </lectures/lecture3/l3_index>`

   Zhang's Method
      The standard technique for camera intrinsic calibration:
      photograph a planar checkerboard from many angles, detect the
      corners, and solve for the intrinsic matrix and the distortion
      coefficients. :doc:`L2 </lectures/lecture2/l2_index>`
