====================================================
Changelog
====================================================

All notable changes to the ENPM818Z Fall 2026 course documentation are recorded here.


.. dropdown:: v2.2.0 -- L3 Released (2026-09-12)
   :icon: tag
   :class-container: sd-border-success
   :open:

   Lecture 3 is now published. It was previously index only, with its
   notes, exercises, quiz and references held back while they were written.

   .. rubric:: Lecture 3: Probabilistic State Estimation & Fusion

   - **New Terminology section.** Variance, standard deviation, uncertainty,
     noise, bias and confidence are each defined before they are used, with
     worked numbers rather than formulas alone. Six GNSS readings of a car
     at a surveyed point run through the whole section, so the same data
     produces the mean, the variance, the sigma bands and the confidence
     interval.
   - **Formal definitions are now cited**: ISO 3534-1:2006 for variance and
     confidence interval, JCGM 100:2008 (GUM) and JCGM 200:2012 (VIM) for
     measurement uncertainty and coverage interval, and Gelman for credible
     regions. VIM is the same document L2 quotes for calibration.
   - **New Notation section** with three symbol tables covering statistics,
     the state and the two models, and the update. It also flags the two
     symbols that do double duty.
   - **The innovation is now written** :math:`\nu` **rather than**
     :math:`y`, because :math:`y` is the across-road coordinate in this
     lecture and the two collided in the NIS and Mahalanobis formulas. Most
     textbooks use :math:`y`, and the notes say so.
   - **New: What a Filter Is.** The word was previously used before it was
     defined. There is now a definition, four reasons a vehicle cannot just
     use the newest reading, and a note on where the name comes from.
   - **New: where uncertainty actually comes from.** :math:`R` is measured,
     reported by the sensor, quoted on a datasheet, or set by you in
     simulation. :math:`Q` is none of those and is always tuned. The notes
     also admit that the worked examples simply hand you a sigma.
   - **New: the lecture contains almost no AI, and says so.** A table dates
     each technique from 1936 to 1999, explains why classical estimation
     still decides where the vehicle thinks it is, and points at L4, L5, L6,
     L9 and L12 for the learned parts of the stack.
   - **Three new figures**: two Gaussians combining into a sharper third,
     the Kalman gain against the noise ratio, and a three step covariance
     ellipse sequence showing prediction growing the ellipse and the update
     shrinking it.
   - **Reordered.** Fusion architectures now comes before combining two
     estimates, so late fusion motivates the question instead of
     interrupting the path from the weighting formula to the Kalman filter.
   - **New roadmap** pairing every section with the question it answers, and
     a transition block between each pair of sections.
   - **Corrected a contradiction with L2.** An earlier draft had students
     run the tracker under CARLA weather presets. L2 measured that CARLA
     does not model LiDAR attenuation, so the exercise now says plainly that
     any degradation comes from a constant you inserted yourself.
   - Tempe is recalled in full, with the NTSB/HAR-19/03 timings, and is
     placed as the third question the other two depend on.

   .. rubric:: Exercises, Quiz and References

   - **Six exercises.** Exercise 5, the divergence hunt, is the centrepiece:
     a filter that reports 0.115 m of uncertainty while sitting 29.7 m from
     the truth, with a mean NIS of 475 against a band topping out at 5.02.
     Every figure in the exercises was computed and checked, not estimated.
   - Exercise 6 works a data association cost matrix by hand, including one
     detection that the gate rejects for one track and accepts for another.
   - **Quiz expanded to 36 questions** (19 multiple choice, 11 true or
     false, 6 short answer), covering variance, the meaning of a confidence
     level, filter consistency and track lifecycle.
   - **References**: new groups for filter consistency and divergence
     (Bar-Shalom, Fitzgerald, Mehra, Blackman and Popoli) and for the
     formal definitions above.

   .. rubric:: Site-wide

   - **Glossary: 57 new terms**, taking it from 189 to 246. L3 coverage goes
     from 12 tagged entries to 57, and L2 from 17 to 37. A **Z** section was
     added for Zero-Doppler Filtering and Zhang's Method, and the A to Z
     navigation line now includes it.
   - ``conf.py`` no longer excludes the L3 pages. L4 to L14 remain index
     only.
   - Fixed a verification step in :doc:`Using CARLA from Python
     </carla/carla-python>` that told students to check their install with
     ``carla.__version__``, which the 0.9.16 wheel does not define and which
     therefore always raised ``AttributeError``.


.. dropdown:: v2.1.0 -- L1 Rewritten from Slide Deck v1.0 (2026-09-03)
   :icon: tag
   :class-container: sd-border-success

   Lecture 1 was rewritten to match the **L1 slide deck v1.0**, and the
   syllabus and glossary were brought in line with it. L2--L14 are now
   index-only while their content is revised.

   .. rubric:: Lecture 1: Course Introduction & AV Landscape

   - **Corrected two widely misquoted figures.** Road deaths updated to
     ~1.19 million per year (WHO 2023). The "94% of crashes are caused by
     driver error" claim was replaced with what the NHTSA study actually
     found -- the *critical reason*, the last event in the causal chain --
     and an explanation of why the original phrasing is wrong. Removed the
     single-point market-size forecast in favour of a note that such
     forecasts differ by a factor of ten.
   - **New terminology sections**: the six DDT subtasks with the lecture
     that teaches each, the DDT fallback (both triggers, and why leaving the
     ODD is not a fault), and the minimal risk condition as a *design
     artifact* with a table of candidate MRCs and the assumption each hides.
   - **Rewrote the SAE levels** as two tables split at the standard's own
     dividing line, plus a new "Three Things the Levels Are Not" section
     (not a quality ranking, not an answer to "what can it do", not what the
     badge says).
   - **New**: the long tail and why simulation is a necessity rather than a
     convenience; disengagement rates and why miles-per-disengagement is
     close to useless as a comparison.
   - **New**: *From Concept to Public Roads* -- the seven-stage pipeline
     (Framework, Specify, Build, Validate, Argue, Approve, Operate) with
     seven sequence diagrams, HARA/SOTIF/TARA and what each produces, and
     the safety case.
   - **Rewrote both case studies** as diagnose-before-the-reveal exercises
     with the findings behind dropdowns. Tempe now identifies *tracking* as
     the technical heart and includes the full NTSB multi-causal finding;
     the October 2023 pullover incident is framed around the MRC as a design
     artifact and as a SOTIF hazard.
   - **New**: *Where the Simulation Ends* -- what CARLA models well, roughly
     and not at all, and why "0.83 mAP" is a claim about CARLA rather than
     about driving.
   - Updated the industry landscape: Level 3 has contracted (Mercedes Drive
     Pilot and BMW Personal Pilot withdrawn during 2026), and per-company
     ride counts were removed in favour of structural observations, since
     those figures change quarterly.
   - Added the ADS pipeline figure mapping each stage to its lecture and
     group project.

   .. rubric:: Exercises and Quiz

   - **Both are now explicitly marked not submitted and not graded**, and
     distinguished from the five graded in-class quizzes.
   - Exercises: six instead of five. New -- classify five anonymized real
     systems by SAE level; write an ODD then find three scenarios it lets
     through that you did not intend; choose an MRC for four situations
     (one of which has no safe answer); diagnose a shadow-braking failure as
     26262 vs. SOTIF. Each now ends with a reasoning box.
   - Quiz: 15 MC + 10 T/F + 5 essay, revised throughout. Removed questions
     resting on perishable deployment figures; added the DDT subtasks,
     fallback triggers, MRC assumptions, the levels-are-not framing, the
     94% misquote, disengagement denominators, the safety case, and the fact
     that a vehicle is still Level 2 throughout Stage 4.

   .. rubric:: Glossary

   - Added: AEB, Conspicuity, DDT Fallback, Disengagement, Driving Automation
     Feature, Fallback-Ready User, Geofence, OEDR, Remote Assistance, Remote
     Driving, Safety Case, TARA, Triggering Condition, UNECE R157 -- all
     tagged to L1.
   - **Corrected MRC**, which previously described it as a response to a
     critical system failure only; leaving the ODD reaches it too, and the
     entry now covers the design-artifact framing. Re-tagged L1 · L14.
   - Expanded DDT to the six J3016 subtasks. Softened the UNECE GTR entry to
     match the deck's more cautious wording.
   - Lecture tags for L2--L14 now point at each lecture's **index** page
     rather than its lecture page, so they keep resolving while that content
     is held back. L1 tags still point at the lecture page.

   .. rubric:: Syllabus

   - Grade breakdown replaced with the six-component split (GP1 10.2%,
     GP2 27.2%, GP3 17.0%, GP4 13.6%, Final Report 12.0%, Quizzes 20.0%).
   - **New**: peer review at 40% of each individual project grade, the Week 3
     team charter, letter-grade cutoffs, the regrade policy, and the
     generative AI policy with its disclosure requirement.
   - Schedule updated: teams form in **Week 3** (was Week 2) after an
     individual pass/fail setup milestone, and quizzes move to weeks 4, 6, 9,
     12 and 14.
   - Hardware minimum raised to an NVIDIA GPU with 8 GB VRAM and 16 GB RAM,
     with a note that a VM is not adequate.

   .. rubric:: Lectures 2--14

   - Each lecture now publishes **only its index page**. The lecture notes,
     exercises, quiz and references are excluded from the build via
     ``exclude_patterns`` in ``conf.py`` and carry a "materials in revision"
     note. No source files were deleted -- removing a lecture's entry from
     ``exclude_patterns`` republishes it.


.. dropdown:: v2.0.0 -- Full Curriculum Released: L4--L13 (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   Complete documentation for all 14 lectures of the ENPM818Z Fall 2026
   curriculum.

   .. rubric:: Lecture 4: Perception II -- BEV Perception & Occupancy Networks

   - BEV motivation, Lift-Splat-Shoot (LSS), BEVFormer (spatial/temporal
     attention), 3D occupancy networks, multi-camera fusion, nuScenes
     benchmarks, Tesla's BEV approach.

   .. rubric:: Lecture 5: Perception III -- Segmentation, Tracking & Temporal Reasoning

   - U-Net, DeepLabv3+/ASPP, instance and panoptic segmentation, SORT,
     DeepSORT, ByteTrack, tracking metrics (MOTA/MOTP/IDF1/HOTA),
     temporal reasoning methods.

   .. rubric:: Lecture 6: Multi-Sensor Fusion

   - Fusion architectures (early/intermediate/late), Kalman Filter
     predict-update cycle with full equations, EKF (Jacobian), UKF (sigma
     points), particle filter, filter comparison, data association
     (NN/GNN/JPDA/MHT), cross-attention fusion (BEVFusion), CARLA code.

   .. rubric:: Lecture 7: Localization & SLAM

   - GNSS/RTK, dead reckoning, visual/LiDAR odometry, EKF and particle
     filter localization, SLAM frontend (ICP, feature extraction,
     keyframes), SLAM backend (pose graph optimization, loop closure),
     LOAM/LeGO-LOAM/LIO-SAM/KISS-ICP, evaluation metrics (APE/RPE).

   .. rubric:: Lecture 8: Motion Planning

   - Planning hierarchy, bicycle model, Dijkstra, A*, RRT/RRT*, PRM,
     lattice planners, collision detection, diffusion-based planning
     (Diffusion Planner, DiffusionDrive), algorithm comparison.

   .. rubric:: Lecture 9: Trajectory Planning & Control

   - Path vs. trajectory, polynomial/spline generation, optimization-based
     planning, MPC (formulation, receding horizon), Pure Pursuit, Stanley
     controller, PID, controller comparison, emergency maneuvers.

   .. rubric:: Lecture 10: Prediction & Decision-Making

   - Trajectory prediction (physics/maneuver/interaction-aware),
     transformer-based prediction, multi-modal futures, behavior planning
     (state machines), imitation learning, DAgger, traffic scenarios.

   .. rubric:: Lecture 11: End-to-End Driving & Foundation Models

   - Modular vs. E2E debate, UniAD, DriveTransformer, VLA models
     (Alpamayo, DriveVLM), chain-of-thought reasoning, Tesla FSD v12,
     NVIDIA RL approach, safety/interpretability concerns.

   .. rubric:: Lecture 12: World Models & Simulation

   - World model definition, video prediction transformers, GAIA-3,
     NVIDIA Cosmos, Vista, generative scenario generation, sim-to-real
     gap, model-based planning (Dreamer), CARLA vs. world models.

   .. rubric:: Lecture 13: System Integration, Safety & Industry Outlook

   - Full AV stack architecture, ROS 2/DDS middleware, real-time
     constraints, ISO 26262 (ASIL, V-model), SOTIF, UNECE GTR on ADS,
     cybersecurity (ISO/SAE 21434), V2X (DSRC/C-V2X), industry outlook
     (US vs. China), robotaxi economics, ethics/liability, career paths,
     course summary.

   .. rubric:: Other Changes

   - Removed all old ENPM605 content from lecture4/ through lecture8/.
   - Created new directories for lecture9/ through lecture13/.
   - Updated lectures/index.rst toctree with all 14 lectures.
   - Each lecture includes: index, lecture notes, quiz (10 MC + 5 T/F +
     3 essay with hidden answers), and categorized references.


.. dropdown:: v1.2.0 -- L2 and L3 Documentation Released (2026-04-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Lecture 2: Sensor Technologies & Calibration

   - Lecture notes covering: complementarity principle (Luo 1989), camera
     systems (telephoto, fisheye, stereo, monocular depth), LiDAR (ToF,
     mechanical vs. solid-state), RADAR (Doppler effect, imaging radar,
     stationary object filtering risk), IMU (drift) and GNSS (signal
     blockage), IMU+GNSS fusion, intrinsic calibration (camera matrix K,
     distortion coefficients), extrinsic calibration (6-DOF transformation),
     sensor placement and coverage patterns, failure mode analysis (single
     point of failure, degraded mode, MRC), design trade-offs ($5K budget
     for highway vs. urban), industry sensor configurations (Waymo, Tesla,
     Cruise, Aurora, Mobileye).
   - Quiz: 15 multiple choice, 10 true/false, 5 essay questions with
     hidden answers.
   - References: sensor technologies, calibration tools, depth estimation,
     industry reports, textbooks.

   .. rubric:: Lecture 3: Perception I -- Object Detection (YOLO to DETR)

   - Lecture notes covering: perception in the AV stack (sensing ->
     perception -> planning -> control), perception inputs/outputs,
     taxonomy of perception tasks (low/mid/high-level), deep learning
     revolution (AlexNet to ResNet), YOLO evolution (v1 to v11 with
     COCO mAP), backbone-neck-head architecture, anchor-based vs.
     anchor-free detection, CIoU loss, training on custom data (with
     Python code), DETR architecture (encoder-decoder, object queries,
     bipartite matching via Hungarian algorithm), Deformable DETR, DINO,
     RT-DETR, YOLO vs. DETR comparison table, ROS 2 perception node
     deployment (with code), preview of BEV/occupancy/E2E.
   - Quiz: 15 multiple choice, 10 true/false, 5 essay questions with
     hidden answers.
   - References: detection papers, DL foundations, segmentation/tracking,
     datasets and benchmarks, tools and frameworks, textbooks.

   .. rubric:: Other Changes

   - Removed old ENPM605 exercise files from lecture2/ and lecture3/.
   - Updated lectures index with 13-lecture v2 curriculum schedule table.
   - Added L2 and L3 to the lectures toctree.


.. dropdown:: v1.1.0 -- Syllabus and Glossary Added (2026-04-01)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Syllabus (new)

   - Grade breakdown (30% assignments, 20% quizzes, 50% final project).
   - 15-week course schedule mapped to 13-lecture curriculum.
   - Cumulative assignment pipeline: A1 (sensors) -> A2 (perception) ->
     A3 (fusion/localization) -> A4 (planning/control) -> Final Project.
   - Final project with standard track (modular ADS) and advanced track
     (end-to-end driving).
   - Required software/tools and hardware recommendations.

   .. rubric:: Glossary (rewritten)

   - Replaced ENPM605 Python glossary with AV-focused terminology from
     L1--L3: 70+ terms across 22 letter sections covering sensors,
     perception, detection architectures, safety standards, CARLA
     concepts, and evaluation metrics.

   .. rubric:: Configuration

   - Set ``header_links_before_dropdown: 7`` to display all navbar items
     without overflow to "More" dropdown.
   - Set ``show_toc_level: 1`` for collapsed right-side TOC with scroll-
     based expansion.


.. dropdown:: v1.0.0 -- Initial Release (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   Initial release of the ENPM818Z Fall 2026 course documentation.

   .. rubric:: Course Structure

   - Course description and landing page (``index.rst``) with prerequisites,
     learning outcomes, grading, and required software.
   - CARLA Simulator section with overview, Python API reference, CLI options,
     troubleshooting, and performance tips.
   - CARLA setup guide for ROS 2 Humble (native Ubuntu 22.04).
   - CARLA setup guide for ROS 2 Jazzy (Docker on Ubuntu 24.04).

   .. rubric:: Lecture 1: Course Introduction & AV Landscape

   - Lecture notes covering: automated vehicles overview, key terminology
     (DDT, ODD, OES, ADAS vs. ADS), SAE J3016 levels, current industry
     landscape (2026), technical challenges, safety standards (ISO 26262,
     SOTIF, UNECE GTR), ADS development pipeline, course focus areas,
     course overview and assessment, development environment setup
     (Git, VS Code, Linux shell), and CARLA simulator introduction.
   - Quiz with 10 sample review questions.
   - References page with standards, government/policy, simulation tools,
     industry reports, textbooks, and coding standards.
