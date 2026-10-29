====================================================
Changelog
====================================================

All notable changes to the ENPM818Z Fall 2026 course documentation are recorded here.


.. dropdown:: v2.18.1: Lecture 8 Colors and Clearer Steps (2026-10-29)
   :icon: tag
   :class-container: sd-border-success
   :open:

   .. rubric:: Lecture 8

   - **Figures:** car A and its path are green, the predicted lane paths
     magenta, so the red cross where A's turn crosses the AV's lane stands
     out. The browser hands-on uses the same colors.
   - **How far ahead to predict:** the story comes first, then the reaction
     time, braking time and stopping time, each named and explained. The
     figure shows the obstacle and that the AV is moving.
   - **Lecture page:** clearer wording in the scene, physics models,
     scoring and several futures sections; the 5 s horizon says why it was
     chosen.
   - **Exercises:** Exercise 1's answers explain the average braking speed.
   - **Quiz:** the horizon question's answer gives the 1.83 s to spare.

.. dropdown:: v2.18.0: Lecture 8 Renamed Trajectory Prediction, New Sections (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **New title:** Trajectory Prediction and Behavior Modeling, on the
     lecture, the schedule, the syllabus and the glossary.
   - **Lecture page:** a new section defines trajectory prediction, road
     user, track, trajectory and horizon. The Tempe section has a figure of
     her path against what the ADS predicted, and says why it never
     predicted her crossing. A new section shows the tracker's one step
     against the planner's 50. Three discussions: trusting the
     probabilities, a learned predictor on our streets, and drivers who
     react to the AV.
   - **Figures:** the vehicles are sharp vector icons in every figure and in
     the browser hands-on.
   - **Quiz:** Question 21's answer follows the new Tempe section.
     **Exercises:** Exercise 4's answer says what the planner does with a
     wider region.
   - **Code page:** lists ``vehicle_icons.py`` and its icons.

   .. rubric:: Lecture 7

   - **Next class:** names L8 by its new title.

.. dropdown:: v2.17.0: Publish Lecture 8, Prediction and Behavior Modeling (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Lecture 8 is open:** the lecture, Going Further (appendix), code,
     exercises, quiz and references pages, and the hands-on that runs in the
     browser. The glossary's L8 section is published and its terms link to
     the L8 index.

   .. rubric:: Pre-Read Material

   - **Foxglove:** the reading that goes with L8, a second viewer for ROS 2
     topics, live or recorded, shown on a demo of L8's predictions.

.. dropdown:: v2.16.2: Lecture 8 Figure Label (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Lecture page:** the opening figure's input box names only L5's tracks.
     Still hidden until Lecture 8 is published.

.. dropdown:: v2.16.1: Lecture 8 Introduction (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Lecture page:** the opening note tells how L5's tracks and L7's map
     lead to prediction, and the figure below it lists two outputs: where
     each road user will be and how sure that is, and which of several
     futures, how likely. Still hidden until Lecture 8 is published.

.. dropdown:: v2.16.0: Lecture 8 Hands-On in the Browser (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Code page:** a link to the hands-on running in the browser: one tab for
     each of the four parts, with the same now slider and questions, and a tab
     where you edit ``l8sim.py`` and run every part again. No Python is needed
     on your computer. Still hidden until Lecture 8 is published.

   .. rubric:: Tools

   - **make_l8_handson_html.py:** builds that page from the lecture8 scripts
     of the course's Python repo.

.. dropdown:: v2.15.1: Lecture 8 Wording (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Lecture and Going Further pages:** shorter wording that matches the
     revised slides, and one correction: with no turn ahead, the most likely
     mode does worse than CV (FDE 3.91 against 3.64 m). Still hidden until
     Lecture 8 is published.

.. dropdown:: v2.15.0: Lecture 8 Audit, New Test Set and New Figures (2026-10-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Test set:** the simulated drivers no longer drift above their cruising
     speed before a turn, so every test-set number is new (2476 predictions).
     The pages now say where CV's misses come from (cars braking for a turn)
     and split the 95% region check into straight and turning routes.
   - **New sections:** a graph of the speed each path expects (Step 2),
     calibration of the predicted probabilities, and post-encroachment time
     (PET). New figures show the stopping distance, the dataset windows, when
     each future puts car A in the AV's lane, the calibration check and PET.
   - **Corrections:** the IDM's gap term, the MTR quote, the average of two
     futures, minADE and minFDE, gap acceptance, Waymo's World Decoder, and
     several arithmetic steps. The quiz gains questions on PET and
     calibration; the glossary gains Calibration (Prediction) and
     Post-Encroachment Time. These pages stay hidden until Lecture 8 is
     published.

.. dropdown:: v2.14.2: GP1 Rig Tool Pitch Sign (2026-10-26)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Tools

   - **make_team_configs.py:** ``--answers`` now uses CARLA's sign for the
     camera pitch, so each rig's matrix matches the one CARLA computes from
     the same mounts. The rig table in GP1 is unchanged.

.. dropdown:: v2.14.1: Lecture 8 Wording (2026-10-25)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **Several Futures and Using the Map:** three notes now say plainly what
     minADE and minFDE check, why car A's prediction scores well (under the
     2 m miss threshold), and what A's speed shows. Still hidden until
     Lecture 8 is published.

.. dropdown:: v2.14.0: Lecture 8 Follows the Revised Slides, and a Foxglove Reading (2026-10-25)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 8

   - **All pages** follow the revised slides: Learned Predictors is now part
     of the lecture, with a new section on what Waymo and Tesla say they use;
     ADE and FDE each get a formula; a flowchart shows the plan for car A;
     Step 3 shows the bell curve and reads its formula in words; the IDM is
     split into its acceleration, the gap it wants, and car B by hand. The
     References page groups the learned predictors' sources, and the Code
     page points to the new Foxglove reading. These pages stay hidden until
     Lecture 8 is published.

   .. rubric:: Pre-Read Material

   - **Foxglove: A Second Viewer for ROS 2:** a new reading that goes with
     Lecture 8, with a live demo of the lecture's predictions on CARLA
     (``l8_foxglove_demo``), a layout to import, and six exercises. Hidden
     with Lecture 8.

   .. rubric:: Lectures

   - **Schedule:** L8's Key Concepts list the learned predictors as lecture
     content.

   .. rubric:: Glossary

   - **L8 (not yet published):** new terms Learned Predictor and Marginal
     Prediction.

.. dropdown:: v2.13.0: Lecture 7 Published (2026-10-24)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 7

   - **Route Planning is open:** the lecture, Going Further, the step by
     step searches, code, exercises, quiz and references. One trip in
     Town01, from the map file to a weighted graph, lane change edges in
     Town03, three edge costs, re-planning on GP4's two triggers, and the
     route as maneuvers.

   .. rubric:: Lectures

   - **Schedule:** L1 to L7 are open.

   .. rubric:: Glossary

   - **L7: Route Planning:** the section is published, and its terms link
     to the lecture.

.. dropdown:: v2.12.0: Lectures 7 and 8 Follow the Reviewed Slides (2026-10-24)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 7

   - **All pages** follow the reviewed slides: the pipeline from the map
     file now splits into the toy graph, searched by hand, and the routing
     graph GP4 uses; Town01 has 124 segments; the turn speed comes with a
     worked example and three slides on reading a curve's radius, from the
     map file and from the waypoints. Eight detail slides moved to Going
     Further. The quiz and exercises use only the lecture's main content,
     and a new first exercise finds the trip's start in the map file. The
     Code page quotes the scripts' output: 160 waypoint pairs from
     ``get_topology()``. These pages stay hidden until Lecture 7 is
     published.

   .. rubric:: Lecture 8

   - **Lecture, Going Further, code, quiz, exercises and references** are
     rewritten from the slides: one Town01 junction and three road users,
     physics models, scoring a prediction, several futures, the map's lanes
     with Bayes' rule, and drivers who react to each other. These pages
     stay hidden until Lecture 8 is published.

   .. rubric:: Lectures

   - **Schedule:** the Key Concepts for L7 and L8 list what each lecture
     now covers. L1 to L6 are open.

   .. rubric:: Glossary

   - **L7 (not yet published):** Toy Graph, Waypoint Graph and Weighted
     Graph are new; Routing Graph now means the waypoint graph with lane
     change edges.
   - **L8 (not yet published):** 17 terms from the slides, among them ADE,
     FDE, minADE, minFDE, miss rate, CTRV, the Intelligent Driver Model and
     critical headway.

.. dropdown:: v2.11.0: Lecture 7 Pages Follow the Slides (2026-10-24)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 7

   - **Lecture, appendix, code, quiz, exercises and references** are
     rewritten to follow the slides: one trip in Town01, from the map file
     to a routing graph, lane change edges in Town03, three edge costs,
     re-planning on GP4's two triggers, and the route as maneuvers. These
     pages stay hidden until Lecture 7 is published.

   .. rubric:: Lectures

   - **Schedule:** the Key Concepts for L7 now list what the lecture
     covers.

   .. rubric:: Glossary

   - **L7 (not yet published):** 29 new terms from Lecture 7, among them
     road, carriageway, route, path, trajectory, routing graph, segment,
     junction, edge cost, travel time, hysteresis and maneuver.
     Configuration space moved here from L9, which now lists it under
     "Also used here". A* Search, Dijkstra, Lanelet2 and OpenDRIVE follow
     the lecture's wording.

.. dropdown:: v2.10.1: GP2 Fixes from a Full Check (2026-10-17)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2, weight:** GP2 is graded out of 100 points and counts for 40% of
     the group-project grade, which is 34.0% of the final project grade and
     27.2% of the course grade. The Projects page now lists 100 points for
     GP1 and GP2; the weights did not change.
   - **GP2, individual grade:** 60% team grade for GP2 plus 40% peer review
     score, as before; the page now says "team grade" where it said "project
     grade".
   - **GP2, lectures:** L2 (projection) is listed with L3, L4 and L5.
   - **GP2, Task 2:** start ``ros2 launch`` from the package root, where the
     weights are; ``replay_drive.py`` takes ``--topic <name>`` if your GP1
     camera does not publish on ``/carla/camera/rgb/image``.
   - **GP2, Task 3:** the AP and mAP follow L4's appendix without COCO's
     limit of 100 boxes per image, as ``check_coco.py`` already did.
   - **GP2, data:** ``gt_boxes.load_frame`` reads the depth, semantic and
     meta files and gives the image's path.
   - **GP2, wording:** shorter in a few places; no task, point or date
     changed.

.. dropdown:: v2.10.0: Lecture 6 Matches the Slides (2026-10-17)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 6

   - **Lecture, appendix, quiz, exercises, code and references** follow
     the final slides: scan registration with ICP and a k-d tree, ICP's
     second step in six named steps, four ways to score a scan and which
     one an AV uses when, scenes that cannot pin down the pose, and the
     pose graph built in Python. The pose graph example uses sigmas of
     0.5 m and 0.3 m, as on the slides.
   - Mentions of the removed NIS plot are gone. Figures are the slides'
     current ones.

   .. rubric:: Schedule

   - Lecture 7 is now called **Route Planning**.

.. dropdown:: v2.9.2: SLAM Pages Link Their Code (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Pre-Read Material

   - **SLAM with a LiDAR** and **Visual SLAM** link to the code that
     measured them, ``lecture6/slam`` in the course's Python repository.
     Run it and you get the same numbers.

.. dropdown:: v2.9.1: GP2 Fixes from a Full Check (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2, commands:** the RT-DETR-L check in the submission checklist
     loads ``rtdetr-l.pt``. Results go to ``../results/gp2/`` from the
     package root, where the folder tree puts them. The install uses
     ``python3 -m pip install --user --break-system-packages``.
   - **GP2, tests and grading:** source ROS 2 before the tests. Task 3
     checks with ``check_coco.py`` first; ``grade.py`` also runs the Task 4
     tracker, so it comes once Task 4 works. Run your chosen confidence cut
     last, then copy ``results.json``.
   - **GP2, smaller fixes:** ``*.pt`` in ``.gitignore``, how to record
     ``node_hz.txt``, a CPU note, the Google Drive download tips, a fuller
     submission checklist, ``README.md`` in the folder tree, two L5 line
     ranges, and the ID-switch count in a figure's description.
   - **GP1:** the folder name uses your team number (``GP1_Team3``), and
     the rig table says which rig each team has (Team1 has rig A, up to
     Team5 with rig E).
   - **Projects page:** GP1 and GP2 are posted.

   .. rubric:: Syllabus and site

   - Ranges and pauses written with words instead of dashes, in the
     syllabus and the projects page. No date changed.
   - The tooltips of the top bar icons are readable in dark mode.
   - The GP2 pre-read is marked "read before you start GP2".

.. dropdown:: v2.9.0: SLAM Reading Pages (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Pre-Read Material

   - **New: SLAM with a LiDAR.** The SLAM problem, EKF-SLAM, FastSLAM and
     grid maps, and graph SLAM solved by Gauss-Newton, with a LiDAR front
     end and Scan Context loop detection. Every number is measured on a
     simulated world or on the L6 drive.
   - **New: Visual SLAM.** The camera model, ORB features, stereo depth,
     PnP tracking, a bag of visual words and a robust back end, measured on
     the L6 route recorded with a stereo camera.
   - The pre-read titles no longer start with "Pre-Read:".

   .. rubric:: Lectures

   - **L6:** the SLAM section links to the two new reading pages.

   .. rubric:: Projects

   - **GP2:** the At a Glance box links to the starter code. Before copying
     the starter, a warning shows how to check that none of its files
     already exists in your package. The test command is explained part by
     part.

.. dropdown:: v2.8.7: Teams of Three (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Syllabus and projects

   - **Teams have 3 students**, not 4: the syllabus, the projects page and
     GP1 to GP4 now say so. Teams form in Week 3.
   - **GP1:** the suggested schedule's total is 35 person-hours, the sum of
     its steps, about 12 hours each for a team of three.
   - **GP2:** how a team of three splits the four coding tasks, and "The
     Situation" now sits in one box.

.. dropdown:: v2.8.6: GP2 Opening Image (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2:** an opening image, as on GP1: the night street, the
     perception lead's three questions, and the two detectors' boxes.

.. dropdown:: v2.8.5: Project Summary Boxes Follow the Theme (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP1 and GP2:** the "At a Glance" box was dark in light mode. It now
     follows the light and dark themes.

.. dropdown:: v2.8.4: GP2, Add the Instructor as a Collaborator (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2, Submission:** add the instructor, GitHub user ``rubixcubic``, as
     a collaborator on your private repository. It is now a step of its own
     and an item on the checklist.

.. dropdown:: v2.8.3: GP2, Your Archive's Name (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2, Your Team's Drives:** your archive is named after your team
     number on Canvas, for example ``team_3_drives.tar`` for Team3.

.. dropdown:: v2.8.2: GP2, Check Your Download (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP2, Your Team's Drives:** a new step checks that your archive
     downloaded completely (``SHA256SUMS``, in the same folder as the
     archives). The page now gives the archive sizes: 1.1 GB to 2.8 GB.

.. dropdown:: v2.8.1: Quiz Answers Hidden Until You Open Them (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Quizzes

   - **Lectures 3 to 6:** the correct option of a multiple-choice question
     was printed in bold, so the answer showed before you opened its box.
     All options now look the same; the answer is only in the box.

.. dropdown:: v2.8.0: Lecture 6 and GP2 Published (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **Lecture 6 (Localization & SLAM)** is published: lecture notes, Going
     Further, the hands-on code page, quiz, exercises and references. The
     glossary's Lecture 6 terms now link to it.
   - **Lecture 4 and the glossary:** "mAP\@0.5" showed as an email link; it
     is plain text again.

   .. rubric:: Projects

   - **GP2: Perception (YOLO vs. RT-DETR)** is posted. You grade the two
     pretrained detectors on your team's own recorded drives, by day and by
     night, and track their detections in the image.

   .. rubric:: Pre-read

   - **New: Grading a Detector and a Tracker.** IoU, precision and recall,
     AP, mAP\@0.5 and mAP\@0.5:0.95, ID switches and MOTA, one step at a
     time. Read it before GP2, Task 3.

.. dropdown:: v2.7.4: Projects in Preparation (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Projects

   - **GP3 and GP4** are being updated to match GP2. They stay hidden;
     nothing new to open yet.

.. dropdown:: v2.7.3: GP2 Moves to Wednesday, October 14 (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Syllabus

   - **GP2 is posted on Wednesday, October 14 (Week 7)**, not with GP1's
     deadline on October 11. It is still due on Thursday, October 29.
   - **GP2 trains no models.** It compares the two pretrained detectors
     from L4, YOLOv8s and RT-DETR-L, on your own CARLA drives. The project
     table and the hardware note now say so.

   .. rubric:: Lectures

   - **Lecture 4:** the "This week" box gives the new GP2 date.

.. dropdown:: v2.7.2: Lecture 6 in Preparation, Continued (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **Lecture 6 (Localization & SLAM)** is still being written and stays
     hidden; nothing new to open yet.

.. dropdown:: v2.7.1: Lecture 6 in Preparation (2026-10-11)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **Lecture 6 (Localization & SLAM)** is being written. Its pages stay
     hidden until its slides are final; nothing new to open yet.

.. dropdown:: v2.7.0: Lectures Renumbered, 13 in Total (2026-10-10)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture numbers

   - **The lectures after L5 move down by one**, so there is no gap: L6 is
     now Localization & SLAM, L7 Navigation & Route Planning, L8 Prediction,
     L9 Motion Planning, L10 Trajectory Generation & Control, L11 End-to-End
     Driving, L12 Simulation & Testing, L13 System Integration & Safety.
     The old L6 (tracking and deep fusion) is part of L5.
   - Updated on the schedule, the lectures page, the pipeline figure in L1,
     the glossary and every lecture page that names another lecture. Older
     entries in this changelog keep the numbers they had at the time.
   - **Glossary filter:** one button per published lecture.

.. dropdown:: v2.6.0: Lecture 5 Published (2026-10-10)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 5: Perception II, 3D Detection, BEV, Fusion & Tracking

   - **Lecture notes** for the whole deck: 3D detection, segmentation, BEV
     and occupancy, fusion, and tracking.
   - **New page: Going Further**, the deck's appendix (inside CenterPoint,
     one pixel onto the grid, Lift and Splat by hand, BEVFormer, the match
     distance, tracking in industry).
   - **Quiz** (38 questions) and **exercises** (7) on the class material,
     and **references** for every source the slides cite.

.. dropdown:: v2.5.0: Lectures 6 to 14 Hidden, GP1 Date, L5 Overview (2026-10-09)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lectures

   - **Lectures 6 to 14 are hidden** until their slides match the syllabus.
     They open one at a time; the Lectures page still lists the plan.
   - **L5 overview rewritten** to match the deck: 3D detection,
     segmentation, BEV and occupancy, fusion and tracking, with five
     learning objectives. The next lecture is L7, Localization and SLAM.
   - **L5 code page:** the tracking exercise's totals corrected to the
     table students work from (NN 13.0 or 11.3, GNN 11.3).
   - **Figures** in L3 and L5 that were transparent now have a white
     background, so they read on the dark theme.

   .. rubric:: Syllabus and assignments

   - **GP1 is due, and GP2 is posted, on Sunday, October 11**: on the
     schedule, the GP1 page, the assignments page and the L4 overview.

   .. rubric:: Glossary

   - **Duplicates merged** (EKF, UKF, extrinsic and intrinsic calibration,
     complementarity, time of flight), five entries no lecture covers
     removed, and every dash taken out.

.. dropdown:: v2.4.0: New Look, Colored Schedule and a Larger Glossary (2026-10-09)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Site

   - **New logo** in the navbar, one for each theme. The navbar text next to
     it is gone, since the logo already names the course.
   - **Light theme** uses a warm sand palette.
   - **The version menu** (bottom right) follows the site's theme, with
     rounded corners.
   - **Course code:** the home page links the two code repositories,
     ``enpm818z-fall-2026-carla-python`` and ``enpm818z-fall-2026-carla-ros``.

   .. rubric:: Syllabus and pre-reads

   - **Course schedule in color:** pre-reads, quizzes and assignments each
     have their own color, and the Thanksgiving recess row is tinted.
   - **Pre-reads in the schedule**, in the week each one is due.
   - **Further reading** added to the Development Environment and
     Automotive Cybersecurity pre-reads.

   .. rubric:: Lecture 3

   - **Matched to the deck:** the reading slide "Matrices can only scale and
     add" is now on the lecture page; the particle filter figure text and the
     UKF worked example agree with the deck.
   - **Exercise 3** states the motion-model rules it uses, so it no longer
     depends on the appendix.

   .. rubric:: Glossary

   - **108 new terms** from L1 to L4 and the L5 code page, and 31 entries
     corrected against the lectures.

.. dropdown:: v2.3.0 -- L3 Updated to Slide Deck v3.0 (2026-10-04)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: Lecture 3: Probabilistic State Estimation & Sensor Fusion

   - **Lecture notes rewritten to follow the v3.0 deck**: the tunnel example
     with sign matches, the Kalman filter step by step, what breaks its
     assumptions, the EKF, and the NIS test. All figures now come from the
     deck.
   - **New page: Going Further**, the deck's appendix (worked models, the
     UKF and the particle filter in detail, notation).
   - **Quiz and exercises rebuilt** on the class material only; nothing
     from the appendix is tested.
   - **Glossary**: 23 new L3 terms; data association and fusion
     architectures moved to L6.

.. dropdown:: v2.2.0 -- L3 Released (2026-09-12)
   :icon: tag
   :class-container: sd-border-success

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
